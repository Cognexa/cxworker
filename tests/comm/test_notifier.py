import gevent


def test_notifier(notifier):
    jobs_done = 2

    def work():
        nonlocal jobs_done
        gevent.sleep(0.5)
        jobs_done -= 1
        notifier.notify()
        gevent.sleep(0.5)
        jobs_done -= 1
        notifier.notify()

    gevent.spawn(work)

    assert jobs_done == 2
    notifier.wait_for(lambda: jobs_done == 0)
    assert jobs_done == 0
    gevent.sleep(0.2)
