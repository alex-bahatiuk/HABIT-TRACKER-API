package com.example.habittracker.repository

import com.example.habittracker.api.ApiClient
import com.example.habittracker.model.Habit
import com.example.habittracker.model.HabitCreate
import com.example.habittracker.model.Token
import com.example.habittracker.model.User
import com.example.habittracker.model.UserCreate
import com.example.habittracker.model.HabitCheckRequest
import com.example.habittracker.model.HabitStatusResponse

class HabitRepository {

    private val api = ApiClient.retrofit.create(
        com.example.habittracker.api.HabitApi::class.java
    )

    suspend fun register(user: UserCreate): User {
        return api.register(user)
    }

    suspend fun login(email: String, password: String): Token {
        return api.login(email, password)
    }

    suspend fun getCurrentUser(token: String): User {
        return api.getCurrentUser("Bearer $token")
    }

    suspend fun getHabits(token: String): List<Habit> {
        return api.getHabits("Bearer $token")
    }

    suspend fun createHabit(
        token: String,
        habit: HabitCreate
    ): Habit {
        return api.createHabit("Bearer $token", habit)
    }

    suspend fun deleteHabit(
        token: String,
        habitId: Int
    ) {
        api.deleteHabit("Bearer $token", habitId)
    }

    suspend fun checkHabit(
        token: String,
        habitId: Int,
        day: String
    ) {
        api.checkHabit(
            token = "Bearer $token",
            habitId = habitId,
            request = HabitCheckRequest
                (day = day)
        )
    }

    suspend fun uncheckHabit(
    token: String,
    habitId: Int,
    day: String
    ) {
    api.uncheckHabit(
        token = "Bearer $token",
        habitId = habitId,
        day = day
    )
    }
    suspend fun getTodayStatus(
    token: String,
    habitId: Int,
    day: String
    ): HabitStatusResponse {
        return api.getTodayStatus(
        token = "Bearer $token",
        habitId = habitId,
        day = day
    )
    }
}