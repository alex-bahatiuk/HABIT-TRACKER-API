package com.example.habittracker.model

data class RegisterRequest(
    val email: String,
    val password: String
)

data class UserResponse(
    val id: Int,
    val email: String
)

data class TokenResponse(
    val access_token: String,
    val token_type: String
)
