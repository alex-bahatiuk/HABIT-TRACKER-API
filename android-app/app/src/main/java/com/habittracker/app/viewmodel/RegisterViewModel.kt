package com.habittracker.app.viewmodel

import androidx.lifecycle.ViewModel
import com.habittracker.app.api.ApiClient
import com.habittracker.app.model.RegisterRequest
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
