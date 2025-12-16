import db from "./DB";

db.prepare(`
  CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    fullname TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    age INTEGER NOT NULL,
    role TEXT NOT NULL DEFAULT 'ETUDIANT',
    major TEXT NOT NULL,
    level INTEGER NOT NULL
                                      
  )
`).run();

console.log("Students table ready");
