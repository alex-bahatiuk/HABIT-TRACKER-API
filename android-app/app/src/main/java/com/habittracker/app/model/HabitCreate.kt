package com.habittracker.app.model

data class HabitCreate(
    val name: String,
    val target_per_week: Int?
)