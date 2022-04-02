#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
Test of asyncio loop and tasks from O'Reilly "Using Asyncio in Python" book.

This program shows 2 possibilities:
 1- One task shuts down other tasks when it has finished,
 2- Signal shuts down all tasks

 For both cases:
    Waiting 'except CancelledError' of all tasks have fully finished

"""

import asyncio

from signal import SIGINT, SIGTERM

import uvloop


async def one__running_for_ever():
    """Stop running if Cancelled."""
    try:
        while True:
            print('Task one__running_for_ever is running...')
            await asyncio.sleep(0.5)

    except asyncio.CancelledError:
        print('Task one__running_for_ever got CancelledError')
        for i in range(3, 0, -1):
            print('Task one__running_for_ever CancelledError '
                  f'is shutting down...{i}')
            await asyncio.sleep(1)
        await asyncio.sleep(2)
        print('Task one__running_for_ever CancelledError has finished')


async def two__stop_after_job_done():
    """First to stop and then trigger cancelling for other tasks."""
    try:
        for i in range(3, 0, -1):
            print(f'Task two__stop_after_job_done {i}')
            await asyncio.sleep(1)

        print('Task two__stop_after_job_done has finished')
        print('Task two__stop_after_job_done cancelling other tasks')
        for task in asyncio.all_tasks():
            task.cancel()

    except asyncio.CancelledError:
        print('Task two__stop_after_job_done got CancelledError')
        await asyncio.sleep(3)
        print('Task two__stop_after_job_done CancelledError has finished')


async def three__stop_loop_at_the_end():
    """Last one to stop until stopped by others."""
    try:
        while True:
            print('Task three__stop_loop_at_the_end running')
            await asyncio.sleep(2)

    except asyncio.CancelledError:
        print('Task three__stop_loop_at_the_end got CancelledError')

        # await that all other task has finished before sending stop
        while len(asyncio.all_tasks(loop=asyncio.get_running_loop())) > 1:
            await asyncio.sleep(1)
            print('Task three__stop_loop_at_the_end awaiting to stop')

        asyncio.get_running_loop().stop()
        print('Task three__stop_loop_at_the_end CancelledError has finished '
              'and has stopped the loop')


def handler(signal):
    """Handle system signals for cancellation.

    Args:
        sig (signal): System signal
    """
    print(f'Got signal: {signal!s}, shutting down all tasks.')
    loop.remove_signal_handler(SIGTERM)
    loop.add_signal_handler(SIGINT, lambda: None)
    for task in asyncio.all_tasks():
        task.cancel()


if __name__ == '__main__':

    uvloop.install()
    loop = asyncio.get_event_loop()

    for sig in (SIGTERM, SIGINT):
        loop.add_signal_handler(sig, handler, sig)

    loop.create_task(one__running_for_ever())
    loop.create_task(two__stop_after_job_done())
    loop.create_task(three__stop_loop_at_the_end())
    loop.run_forever()

    tasks = asyncio.all_tasks(loop=loop)
    for t in tasks:
        t.cancel()

    group = asyncio.gather(*tasks, return_exceptions=True)
    loop.run_until_complete(group)

    print('Task main has finished\n')
    loop.close()
