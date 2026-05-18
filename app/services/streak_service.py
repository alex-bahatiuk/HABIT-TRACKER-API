from datetime import date, timedelta

def calculate_weekly_stats(
    completed_dates: list[date],
    current_date: date,
    weekly_target: int = 3,
) -> dict:
    start_of_week = current_date.fromordinal(
        current_date.toordinal() - current_date.weekday()
    )
    end_of_week = start_of_week.fromordinal(start_of_week.toordinal() + 6)

    current_week_count = sum(
        1 for d in completed_dates
        if start_of_week <= d <= end_of_week
    )
    
    streak = calculate_completed_week_streak(
        completed_dates=completed_dates,
        current_date=current_date,
        weekly_target=weekly_target,
    )

    checked_last_days = sum(
        1 for d in completed_dates
        if current_date - timedelta(days=30) <= d <= current_date
)
    return {
        "streak": streak,
        "checked_last_days": checked_last_days,
    }

def calculate_completed_week_streak(
    completed_dates: list[date],
    current_date: date,
    weekly_target: int,
) -> int:
    current_week_start = current_date.fromordinal(
        current_date.toordinal() - current_date.weekday()
    )

    streak = 0
    week_start = current_week_start.fromordinal(current_week_start.toordinal() - 7)

    while True:
        week_end = week_start.fromordinal(week_start.toordinal() + 6)

        week_count = sum(
            1 for d in completed_dates
            if week_start <= d <= week_end
        )

        if week_count >= weekly_target:
            streak += 1
            week_start = week_start.fromordinal(week_start.toordinal() - 7)
        else:
            break

    return streak