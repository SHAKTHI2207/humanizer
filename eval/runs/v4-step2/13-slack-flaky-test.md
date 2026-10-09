It's the system clock. test_checkout_total depends on it and fails when it runs near midnight UTC. I'll pin the clock with freezegun and have a PR up today.
