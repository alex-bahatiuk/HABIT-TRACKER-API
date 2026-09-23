package com.habittracker.app.model

data class Habit(
    val id: Int,
    val name: String,
    val target_per_week: Int?
)
