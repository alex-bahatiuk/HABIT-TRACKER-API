import { deleteHabit } from "../api/habitsApi";

function HabitCard({ habit, onComplete, onDelete }) {
    const handleDelete = async () => {
    await deleteHabit(habit.id);
    onDelete(habit.id);
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