<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
#   Table of Content

- [Transaction](#transaction)
- [Concept](#concept)
- [A typical transaction running phases](#a-typical-transaction-running-phases)
  - [For tx killed in phase 0, 1, 2, 3](#for-tx-killed-in-phase-0-1-2-3)
    - [Condition:](#condition)
    - [Solution: Abort](#solution-abort)
  - [For tx killed in phase 4, 5, 6, 7, 8, 9](#for-tx-killed-in-phase-4-5-6-7-8-9)
    - [Condition:](#condition-1)
    - [Solution: re-apply journal and unlock](#solution-re-apply-journal-and-unlock)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Transaction

> In this doc `tx` is an abbreviation of `transaction`.


# Concept


In the following chart it shows how resource status changes when tx action is
taken.

Normally tx resources includes:

-   tx-lock: indicates if a tx is still running. There is only 1 tx-lock for
    each tx.

    It is a ephemeral node in zk.

-   key-locks: for each record involved in a tx there is a corresponding lock 
    to protect it.

    Each key-lock is a normal node in zk(not ephemeral).

-   journal: is a zk node that stores all modifications of a tx.

    Journal write is atomic.
    And the zk-node of a journal is named with txid.

-   keys: records.

    Each record is identified by a key.
    Data of a record is stored in a zk-node.

-   committed-flag: stores tx-id status: COMMITTED, ABORTED or
    PURGED.

    In our implementation all tx status are stored together in one zk-node:
    `txidset`.

    `txidset` is a dict of 3 `rangeset` for COMMITTED, ABORTED and PURGED:

    ```yaml
    COMMITTED: [[1, 2], [4, 5]]
    ABORTED:   [[2, 4]]
    PURGED:    [[1, 3]]
    ```

    -   COMMITTED:
        -   If a tx completely committed, its txid is add to `txidset["COMMITTED"]`.
        -   If a tx aborted(for any reason) **AFTER** journal was written, there is a
            chance another tx detected this dead tx and re-do it.
            In this case, eventually the dead tx will be committed, and will be
            added into `txidset["COMMITTED"]`.

    -   ABORTED:
        -   If a user explicitly aborts a tx(by calling `tx.abort()`), the txid
            is added into `txidset["ABORTED"]`.
        -   If a tx aborted(for any reason) **BEFORE** journal was written,
            another tx will find this dead tx by acquiring a key-lock that the
            dead tx had been held.
            In this case, the other tx will add the dead txid into `txidset["ABORTED"]`.

    -   PURGED:
        -   In order to recycle storage space in zk, there is a background
            process cleans up journal. If a journal is removed, its txid is
            added into `txidset["PURGED"]`.

    **ABORTED txid set and COMMITTED txid set has no common element**:
    A tx is either COMMITTED or ABORTED.

    > It is possible a dead txid not in either of COMMITTED or ABORTED, when no
    > one has discovered this tx was dead(another tx will find a dead tx when
    > trying to acquire a key-lock which is held by dead tx, and there is a
    > background process periodically looks up for dead tx).

    A txid that is added into `txidset["PURGED"]` will not be removed from
    ABORTED or COMMITTED(not necessary).

    Thus all journals those are current available in zk are:
    `txidset["COMMITTED"] - txidset["PURGED"]`.


# A typical transaction running phases

```
|     |  action \ resource | tx-lock | 3 key-locks | journal | 3 keys | committed-flag |
| :-- | :--                | :--     | :--         | :--     | :--    | :--            |
| 0   | tx_begin()         | √       |             |         |        |                |
| 1   | lock_get()         | √       | √           |         |        |                |
| 2   | lock_get()         | √       | √√          |         |        |                |
| 3   | lock_get()         | √       | √√√         |         |        |                |
| 4   | write_journal()    | √       | √√√         | √       |        |                |
| 5   | apply(             | √       | √√√         | √       | √      |                |
| 6   | .....)             | √       | √√√         | √       | √√√    |                |
| 7   | unlock_key(        | √       |  √√         | √       | √√√    |                |
| 8   | ..........)        | √       |             | √       | √√√    |                |
| 9   | add_txidset()      | √       |             | √       | √√√    | √              |
| a   | unlock_tx()        |         |             | √       | √√√    | √              |
```

A tx may be killed in any phase, by any reason.

We have corresponding recovery procedure for each phase to guarantee that a tx
either be completely applied or completely aborted.

-   A tx died without finishing phase-4 will be **eventually aborted**.
-   A tx finished phase-4 will be **eventually committed**.

**Any time a tx runner is killed, tx-lock is deleted automatically(by the
definition of ephemeral node). But key-lock will not be deleted
automatically(key locks are not ephemeral zk node)**.

A redo process first re-acquire the tx-lock(in order to ensure no other process
was dealing with this tx), then does the following phase:

## For tx killed in phase 0, 1, 2, 3

Key locks are partially or completely held.

### Condition:

If we found there is **NOT** a journal written, we can be sure that the dead tx
is in phase 0, 1, 2, 3.


### Solution: Abort

Just unlock all seen key locks held by this tx,
because there is no data to commit in journal,
nothing should be applied.

> In these phase there is no way to unlock all keys, because we need to find all
> locked keys in the tx journal, but there is no journal written.
>
> It is possible that a key-lock belonging to a dead tx stays locked for a very
> long time until another tx tries to lock it.

## For tx killed in phase 4, 5, 6, 7, 8, 9

Key locks are all held, and may be partially unlocked.
And changes are partially or fully applied to key records.


### Condition:

If we found a journal for this tx


### Solution: re-apply journal and unlock

-   We apply all changes stored in this journal.

    **Here we must guarantee that re-applying a change has no effect
    on a key record**.

    This is done in the storage layer.

-   Try to release all key locks:

    -   Try to lock it.

    -   If a lock is acquired, just release it.
        **Because a same tx is able to acquire a lock more than one times.**

    -   If a lock is held by others, just skip.

        This means this record has already been unlocked previous and has been locked by other tx.

    This way we release all the key-locks held by a previous dead tx, and leave
    locks held by others intact.

-   Update the `txidset` for this tx, to mark it as COMMITTED.