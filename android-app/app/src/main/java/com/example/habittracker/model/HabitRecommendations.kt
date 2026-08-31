package com.example.habittracker.model

import com.example.habittracker.R

fun recommendedHabits(
    goal: GoalCategory
): List<HabitTemplate> {
    return when (goal) {
        GoalCategory.HEALTH -> listOf(
            HabitTemplate(
                id = "drink_water",
                titleRes = R.string.habit_drink_water
            ),
            HabitTemplate(
                id = "take_walk",
                titleRes = R.string.habit_take_walk
            ),
            HabitTemplate(
                id = "exercise",
                titleRes = R.string.habit_exercise
            ),
            HabitTemplate(
                id = "sleep_on_time",
                titleRes = R.string.habit_sleep_on_time
            ),
            HabitTemplate(
                id = "eat_vegetables",
                titleRes = R.string.habit_eat_vegetables
            )
        )

        GoalCategory.ENERGY -> emptyList()
        GoalCategory.PRODUCTIVITY -> emptyList()
        GoalCategory.MOOD -> emptyList()
        GoalCategory.CONFIDENCE -> emptyList()
        GoalCategory.DISCIPLINE -> emptyList()
    }
}

