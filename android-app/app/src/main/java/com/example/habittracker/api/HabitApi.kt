package com.example.habittracker.api

import com.example.habittracker.model.Habit
import com.example.habittracker.model.HabitCreate
import com.example.habittracker.model.Token
import com.example.habittracker.model.User
import com.example.habittracker.model.UserCreate
import retrofit2.http.Body
import retrofit2.http.DELETE
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.POST
import retrofit2.http.Path
import retrofit2.http.Field
import retrofit2.http.FormUrlEncoded
import com.example.habittracker.model.HabitCheckRequest
import com.example.habittracker.model.HabitStatusResponse
import retrofit2.http.Query

interface HabitApi {

    @POST("auth/register")
    suspend fun register(
        @Body user: UserCreate
    ): User

    @FormUrlEncoded
    @POST("auth/login")
    suspend fun login(
        @Field("username") email: String,
        @Field("password") password: String
    ): Token

    @GET("auth/me")
    suspend fun getCurrentUser(
        @Header("Authorization") token: String
    ): User

    @GET("habits")
    suspend fun getHabits(
        @Header("Authorization") token: String
    ): List<Habit>

    @POST("habits")
    suspend fun createHabit(
        @Header("Authorization") token: String,
        @Body habit: HabitCreate
    ): Habit

    @POST("habits/{habitId}/check")
    suspend fun checkHabit(
    @Header("Authorization") token: String,
    @Path("habitId") habitId: Int,
    @Body request: HabitCheckRequest
    )

    @DELETE("habits/{habitId}/check")
suspend fun uncheckHabit(
    @Header("Authorization") token: String,
    @Path("habitId") habitId: Int,
    @Query("day") day: String
    )
    @GET("habits/{habitId}/today-status")
    suspend fun getTodayStatus(
    @Header("Authorization") token: String,
    @Path("habitId") habitId: Int,
    @Query("day") day:
    String
    ): HabitStatusResponse

    @DELETE("habits/{habitId}")
    suspend fun deleteHabit(
        @Header("Authorization") token: String,
        @Path("habitId") habitId: Int
    )
}