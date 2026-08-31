package com.example.habittracker.model

import androidx.annotation.StringRes
import com.example.habittracker.R

enum class GoalCategory(
    @StringRes val titleRes: Int
) {
    HEALTH(R.string.goal_health),
    ENERGY(R.string.goal_energy),
    PRODUCTIVITY(R.string.goal_productivity),
    MOOD(R.string.goal_mood),
    CONFIDENCE(R.string.goal_confidence),
    DISCIPLINE(R.string.goal_discipline)
}