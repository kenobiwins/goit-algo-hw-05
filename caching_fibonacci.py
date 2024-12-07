def caching_fibonacci():
    cache = {}

    def fibonacci(n: int) -> int:
        if n <= 1:
            return max(0, n)
        if n in cache:
            return cache[n]

        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci
