import { useEffect, useState } from "react";
import { deleteHabit, getHabitStrength } from "../api/habitsApi";

function HabitCard({ habit, onComplete, onDelete }) {
    const handleDelete = async () => {
    await deleteHabit(habit.id);
    onDelete(habit.id);
    <p>
      Strength: {strength === null ? "Loading..." : strength}
    </p>
};
  return (
    <div>
      <h3>{habit.name}</h3>
      <button onClick={handleDelete}>Delete</button>
      <button onClick={() => onComplete(habit.id)}>Complete</button>
    </div>
  );
}

export default HabitCard;