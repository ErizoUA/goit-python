from redis_lru import RedisLRU
import redis

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client, default_ttl=1, max_size=100000)


@cache
def factorial(number: int):
    if number < 0:
        raise ValueError("number must be positive")
    elif number == 0:
        print(f"calculating factorial f({number})")
        return 1
    elif number > 0:
        print(f"calculating factorial f({number})")
        return number * factorial(number - 1)


if __name__ == "__main__":
    print(factorial(7))
    print('===========')
    print(factorial(10))
