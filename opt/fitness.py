def compute_fitness(metrics: dict, lambdas: tuple = (0.1, 0.1, 0.1)) -> float:
    """Compute fitness score from metrics."""
    winrate = metrics.get("winrate", 0.0)
    turns = metrics.get("avg_turns", 0.0)
    damage = metrics.get("avg_damage", 0.0)
    penalties = metrics.get("penalties", 0.0)
    l1, l2, l3 = lambdas
    return winrate - l1 * turns - l2 * damage - l3 * penalties
