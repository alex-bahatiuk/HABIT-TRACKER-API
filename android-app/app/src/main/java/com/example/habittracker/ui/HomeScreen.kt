package com.example.habittracker.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Checkbox
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.habittracker.R
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.TextButton
import androidx.compose.ui.platform.LocalContext
import com.example.habittracker.viewmodel.HabitViewModel
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.habittracker.utils.TokenManager
import androidx.compose.runtime.LaunchedEffect

@Composable
fun HomeScreen() {
    val context = LocalContext.current
    val viewModel: HabitViewModel = viewModel()
    val habits = viewModel.habits
    val token = TokenManager.getToken(context)
    val completedHabits = remember {
    mutableStateListOf<Int>()
    }
    LaunchedEffect(token) {
        if (token != null) {
            viewModel.loadHabits(token)
        }
    }
    LaunchedEffect(habits, token) {
    if (token != null) {
        val day = java.time.LocalDate.now().toString()

        habits.forEach { habit ->
            viewModel.getTodayStatus(
                token = token,
                habitId = habit.id,
                day = day
            ) { isCompleted ->
                if (isCompleted && habit.id !in completedHabits) {
                    completedHabits.add(habit.id)
                }
            }
        }
    }
}

    var showAddDialog by remember {
    mutableStateOf(false)
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp)
    ) {

        Text(
            text = stringResource(R.string.home_greeting),
            fontSize = 30.sp,
            fontWeight = FontWeight.Bold
        )

        Spacer(modifier = Modifier.height(28.dp))

        Text(
            text = stringResource(R.string.home_today),
            fontSize = 22.sp,
            fontWeight = FontWeight.Bold
        )

        Spacer(modifier = Modifier.height(12.dp))

        HorizontalDivider()

        Spacer(modifier = Modifier.height(16.dp))

        habits.forEach { habit ->

    Row(
        modifier = Modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Checkbox(
            checked = habit.id in completedHabits,
            onCheckedChange = { checked ->
                if (checked) {
                    completedHabits.add(habit.id)
                                     if (token != null) {
                    val day = java.time.LocalDate.now().toString()
            viewModel.checkHabit(
                token = token,
                habitId = habit.id,
                day = day
            )
        }
                } else {
                    completedHabits.remove(habit.id)
                    if (token != null) {
                       val day = java.time.LocalDate.now().toString()

             viewModel.uncheckHabit(
                 token = token,
                 habitId = habit.id,
                 day = day
             )
        }
                }
            }
        )

        Text(
            text = habit.name,
            fontSize = 18.sp
        )
    }
}

        Spacer(modifier = Modifier.height(24.dp))

        Button(
            onClick = {
                showAddDialog = true
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text(
                text = stringResource(R.string.home_add_habit)
            )
        }

        Spacer(modifier = Modifier.height(32.dp))

        Text(
            text = stringResource(R.string.home_today_progress),
            fontSize = 20.sp,
            fontWeight = FontWeight.Bold
        )

        Spacer(modifier = Modifier.height(12.dp))

        Text(
             text = "${completedHabits.size} / ${habits.size}",
             fontSize = 24.sp
        )

        Spacer(modifier = Modifier.weight(1f))


        HorizontalDivider()

        Spacer(modifier = Modifier.height(16.dp))

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceAround
        ) {
            Text(stringResource(R.string.home_tab_home))
            Text(stringResource(R.string.home_tab_stats))
            Text("+")
            Text(stringResource(R.string.home_tab_profile))
        }
        if (showAddDialog) {

    var habitName by remember {
        mutableStateOf("")
    }

    AlertDialog(
        onDismissRequest = {
            showAddDialog = false
        },

        title = {
            Text("Add habit")
        },

        text = {
            OutlinedTextField(
                value = habitName,
                onValueChange = {
                    habitName = it
                },
                label = {
                    Text("Habit name")
                },
                singleLine = true
            )
        },

        confirmButton = {
            TextButton(
                onClick = {
                    val name = habitName.trim()

                    if (name.isNotEmpty()) {
                        val token = TokenManager.getToken(context)
                        if (token != null) {
                            viewModel.createHabit(token = token, name = name)
                        }
                        showAddDialog = false
                    }
                }
            ) {
                Text("Add")
            }
        },

        dismissButton = {
            TextButton(
                onClick = {
                    showAddDialog = false
                }
            ) {
                Text("Cancel")
            }
        }
    )
}
    }
}



