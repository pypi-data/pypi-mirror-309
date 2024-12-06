from picarlo.sim import Config, monte_carlo_pi, stringify_the_float


def main() -> None:
    config = Config()

    stringify_the_float(config.num_samples)

    print(f"starting pi carlo with {config.num_samples} samples!")

    pi = monte_carlo_pi(config.num_samples)

    print(f"pi is approximately {pi}")


if __name__ == "__main__":
    main()
