package com.example.habittracker.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.habittracker.model.Habit
import com.example.habittracker.model.HabitCreate
import com.example.habittracker.model.Token
import com.example.habittracker.model.User
import com.example.habittracker.model.UserCreate
import com.example.habittracker.repository.HabitRepository
import kotlinx.coroutines.launch
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue


class HabitViewModel : ViewModel() {

    private val repository = HabitRepository()

    var habits by mutableStateOf<List<Habit>>(emptyList())
        private set

    fun register(
        user: UserCreate,
        onSuccess: (User) -> Unit,
        onError: (Exception) -> Unit
    ) {
        viewModelScope.launch {
            try {
                val result = repository.register(user)
                onSuccess(result)
            } catch (e: Exception) {
                onError(e)
            }
        }
    }

    fun login(
        email: String,
        password: String,
        onSuccess: (Token) -> Unit,
        onError: (Exception) -> Unit
    ) {
        viewModelScope.launch {
            try {
                val result = repository.login(email, password)
                onSuccess(result)
            } catch (e: Exception) {
                onError(e)
            }
        }}

    fun loadHabits(token: String) {
            viewModelScope.launch {
                try {
                    habits = repository.getHabits(token)
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }
        }

    fun createHabit(
            token: String,
            name: String
        ) {
            viewModelScope.launch {
                try {
                    repository.createHabit(
                        token = token,
                        habit = HabitCreate(
                            name = name,
                            target_per_week = null
                        )
                    )

                    habits = repository.getHabits(token)

                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }
        }
    fun checkHabit(
    token: String,
    habitId: Int,
    day: String
) {
        viewModelScope.launch {
            try {
                repository.checkHabit(
                   token = token,
                   habitId = habitId,
                   day = day
            )
            } catch (e: Exception) {
            e.printStackTrace()
            }
        }}
    fun uncheckHabit(
    token: String,
    habitId: Int,
    day: String
) {
    viewModelScope.launch {
        try {
            repository.uncheckHabit(
                token = token,
                habitId = habitId,
                day = day
            )
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
    }
    fun getTodayStatus(
        token: String,
        habitId: Int,
        day: String,
        onResult: (Boolean) -> Unit)
    {
        viewModelScope.launch {
            try {
            val result = repository.getTodayStatus(
                token = token,
                habitId = habitId,
                day = day
            )
            println("STATUS DEBUG: habitId=$habitId day=$day status=${result.status}")
            onResult(result.status == "completed")

        } catch (e: Exception) {
            println("STATUS ERROR: ${e.message}")
            e.printStackTrace()
            onResult(false)
        }
        }
    }
    fun deleteHabit(
    token: String,
    habitId: Int
) {
    viewModelScope.launch {
        try {
            repository.deleteHabit(
                token = token,
                habitId = habitId
            )

            loadHabits(token)

        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
}
}