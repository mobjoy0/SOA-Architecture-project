import express from "express";
import "./database/init";
import studentsRoutes from "./routes/routes";

const app = express();
app.use(express.json());

app.use("/students", studentsRoutes);

app.listen(5049, () => {
    console.log("Server running on http://localhost:5049");
});
