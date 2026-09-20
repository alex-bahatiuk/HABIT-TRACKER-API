package com.example.habittracker.viewmodel

import androidx.lifecycle.ViewModel
import com.example.habittracker.api.ApiClient
import com.example.habittracker.model.RegisterRequest
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.launch
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue

class RegisterViewModel : ViewModel() {
     private val authApi = ApiClient.authApi
     var registrationSuccess by mutableStateOf(false)
         private set
     var registrationError by mutableStateOf(false)
         private set
     fun register(email: String, password: String)
     {
         viewModelScope.launch{
             try{
                  val request = RegisterRequest(email, password)
                  val response = authApi.register(request)
                  registrationSuccess = true
             }    catch (e: Exception) {registrationError = true}
     }
}}
