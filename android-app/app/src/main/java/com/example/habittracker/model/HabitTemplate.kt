package com.example.habittracker.model

import androidx.annotation.StringRes

data class HabitTemplate(
    val id: String,
    @StringRes val titleRes: Int? = null,
    val customTitle: String? = null)
