def grade_episode(info: dict, task: str) -> float:
    targets = {'easy': (40, 3), 'medium': (80, 5), 'hard': (120, 7)}
    t_target, e_target = targets.get(task, (40, 3))
    t_score = min(info['throughput'] / t_target, 1.0)
    e_score = min(info['emergencies'] / e_target, 1.0)
    return round(0.6 * t_score + 0.4 * e_score, 3)