import { useEffect, useState } from "react";
import { deleteHabit, getHabitStrength, skipHabit } from "../api/habitsApi";

function HabitCard({ habit, onComplete, onDelete }) {
    const [strength, setStrength] = useState(null);
    const [todayStatus, setTodayStatus] = useState(null);

    useEffect(() => {
        const fetchHabitStrength = async () => {
            const habitStrength = await getHabitStrength(habit.id);
            setStrength(habitStrength.strength);
        };

        fetchHabitStrength();
    }, [habit.id]);

    const handleDelete = async () => {
    await deleteHabit(habit.id);
    onDelete(habit.id);
};
  return (
    <div>
      <h3>{habit.name}</h3>
      <p>
        Strength: {strength === null ? "Loading..." : strength}
        {todayStatus === "completed" && <p>Completed today</p>}
        {todayStatus === "skipped" && <p>Skipped today</p>}
      </p>
      <button onClick={handleDelete}>Delete</button>
      <button onClick={async () => {await onComplete(habit.id);
                                    setTodayStatus("completed");
              const habitStrength = await getHabitStrength(habit.id);
        setStrength(habitStrength.strength);}}>Complete</button>
      <button onClick={async () => {await skipHabit(habit.id, new Date().toISOString().slice(0, 10));
                                    setTodayStatus("skipped");
              const habitStrength = await getHabitStrength(habit.id);
        setStrength(habitStrength.strength);}}>Skip</button>
    </div>
  );
}

export default HabitCard;