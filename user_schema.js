const mongoose = require("mongoose");

// Define the user schema
const userSchema = new mongoose.Schema({
  username: {
    type: String,
    required: true,
    maxlength: 200,
  },
  age: {
    type: Number,
    required: true,
  },
  score: {
    type: Number,
    required: true,
  },
  question_count: {
    type: Number,
    required: true,
  },
  quiz_date: {
    type: Date,
    default: Date.now, // Set to the current date and time by default
  },
});

// Create a model based on the schema
const User = mongoose.model("User", userSchema);

module.exports = User;
