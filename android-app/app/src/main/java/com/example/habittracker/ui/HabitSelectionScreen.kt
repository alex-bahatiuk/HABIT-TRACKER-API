package com.example.habittracker.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.Checkbox
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.habittracker.R
import com.example.habittracker.model.GoalCategory
import com.example.habittracker.model.HabitTemplate
import com.example.habittracker.model.recommendedHabits


@Composable
fun HabitSelectionScreen(
    onNextClick:() -> Unit
)
{
    val habits = remember {
    mutableStateListOf<HabitTemplate>().apply {
        addAll(
            recommendedHabits(GoalCategory.HEALTH)

        )
    }
}
    val selectedHabits = remember {
        mutableStateListOf<HabitTemplate>()
    }

    var showAddDialog by remember {
        mutableStateOf(false)
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(horizontal = 24.dp, vertical = 32.dp)
    ) {
        Text(
            text = stringResource(R.string.habit_selection_title),
            modifier = Modifier.fillMaxWidth(),
            fontSize = 30.sp,
            fontWeight = FontWeight.Bold,
            textAlign = TextAlign.Center
        )

        Spacer(modifier = Modifier.height(12.dp))

        Text(
            text = stringResource(R.string.habit_selection_description),
            modifier = Modifier.fillMaxWidth(),
            fontSize = 18.sp,
            textAlign = TextAlign.Center
        )

        Spacer(modifier = Modifier.height(24.dp))

        LazyColumn(
            modifier = Modifier.weight(1f),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(
                items = habits,
                key = { habit -> habit.id }
            ) { habit ->
                HabitSelectionItem(
                    habit = habit,
                    isSelected = habit in selectedHabits,
                    onSelectionChange = { isSelected ->
                        if (isSelected) {
                            selectedHabits.add(habit)
                        } else {
                            selectedHabits.remove(habit)
                        }
                    }
                )
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        OutlinedButton(
            onClick = {
                showAddDialog = true
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text(
                text = stringResource(R.string.create_custom_habit)
            )
        }

        Spacer(modifier = Modifier.height(12.dp))

        Button(
            onClick = {
                onNextClick()
            },
            enabled = selectedHabits.isNotEmpty(),
            modifier = Modifier.fillMaxWidth()
        ) {
            Text(
                text = stringResource(R.string.next),
                fontSize = 18.sp
            )
        }
    }

    if (showAddDialog) {
        AddHabitDialog(
            onDismiss = {
                showAddDialog = false
            },

            onAddHabit = { habitName ->
                 val newHabit = HabitTemplate(
                     id = "custom_${System.currentTimeMillis()}",
                      customTitle = habitName
    )

                   habits.add(newHabit)
                selectedHabits.add(newHabit)
                    showAddDialog = false
}
        )
    }
}

@Composable
private fun HabitSelectionItem(
    habit: HabitTemplate,
    isSelected: Boolean,
    onSelectionChange: (Boolean) -> Unit
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Checkbox(
            checked = isSelected,
            onCheckedChange = onSelectionChange
        )

        Text(
            text = habit.titleRes?.let
            { stringResource(it)} ?:
            habit.customTitle.orEmpty(),
            fontSize = 18.sp
        )
    }
}

@Composable
private fun AddHabitDialog(
    onDismiss: () -> Unit,
    onAddHabit: (String) -> Unit
) {
    var habitName by remember {
        mutableStateOf("")
    }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = {
            Text(
                text = stringResource(R.string.create_custom_habit)
            )
        },
        text = {
            OutlinedTextField(
                value = habitName,
                onValueChange = {
                    habitName = it
                },
                label = {
                    Text(
                        text = stringResource(R.string.habit_name)
                    )
                },
                singleLine = true,
                modifier = Modifier.fillMaxWidth()
            )
        },
        confirmButton = {
            TextButton(
                onClick = {
                    val trimmedName = habitName.trim()

                    if (trimmedName.isNotEmpty()) {
                        onAddHabit(trimmedName)
                    }
                },
                enabled = habitName.isNotBlank()
            ) {
                Text(
                    text = stringResource(R.string.add)
                )
            }
        },
        dismissButton = {
            TextButton(
                onClick = onDismiss
            ) {
                Text(
                    text = stringResource(R.string.cancel)
                )
            }
        }
    )
}

