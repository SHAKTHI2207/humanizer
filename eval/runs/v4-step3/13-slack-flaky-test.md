It's the system clock. test_checkout_total depends on the current time, so it fails when CI runs near midnight UTC. I'll pin the clock with freezegun and have a PR up today.
