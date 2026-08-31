package com.example.habittracker.api

import retrofit2.http.Body
import retrofit2.http.Field
import retrofit2.http.FormUrlEncoded
import retrofit2.http.POST
import com.example.habittracker.model.RegisterRequest
import com.example.habittracker.model.TokenResponse
import com.example.habittracker.model.UserResponse

interface AuthApi {

    @FormUrlEncoded
    @POST("auth/login")
    suspend fun login(
        @Field("username") email: String,
        @Field("password") password: String
    ): TokenResponse

    @POST("auth/register")
    suspend fun register(
        @Body request: RegisterRequest
    ): UserResponse
}