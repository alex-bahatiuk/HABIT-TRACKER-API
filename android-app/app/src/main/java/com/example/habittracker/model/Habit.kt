package com.example.habittracker.model

data class Habit(
    val id: Int,
    val name: String,
    val target_per_week: Int?
)
