package com.habittracker.app.model

data class HabitStats(
    val streak: Int,
    val checked_last_days: Int,
    val skipped_last_days: Int,
    val checked_this_week: Int
)

