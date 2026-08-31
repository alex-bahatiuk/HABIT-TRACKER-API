package com.example.habittracker.model

data class HabitCreate(
    val name: String,
    val target_per_week: Int?
)