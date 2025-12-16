import axios from "axios";
import { StudentDTO } from "../models/studentDTO";

const AUTH_SERVICE_URL = "http://localhost:5048/auth";

interface AuthUserResponse {
    id: number;
    password?: string;
}

// Helper function to get headers with token
const getAuthHeaders = (token?: string) => {
    const headers: any = {
        "Content-Type": "application/json"
    };

    if (token) {
        // Ensure no extra spaces in the token
        headers["Authorization"] = `Bearer ${token.trim()}`;
    }

    return headers;
};

export const createStudentAPI = async (data: StudentDTO, token?: string): Promise<AuthUserResponse> => {
    const generatedPassword = generatePassword();

    const response = await axios.post<AuthUserResponse>(
        `${AUTH_SERVICE_URL}/register`,
        {
            username: data.fullname,
            email: data.email,
            password: generatedPassword,
            role: "ETUDIANT"
        },
        {
            headers: getAuthHeaders(token)
        }
    );

    return {
        ...response.data,
        password: generatedPassword
    };
};

export const deleteStudentAPI = async (id: number, token?: string): Promise<void> => {
    await axios.delete(`${AUTH_SERVICE_URL}/delete/${id}`, {
        headers: getAuthHeaders(token)
    });
};

export const updateStudentAPI = async (id: number, data: Partial<StudentDTO>, token?: string): Promise<void> => {
    const updateData: any = {};

    if (data.email) {
        updateData.email = data.email;
    }
    if (data.fullname) {
        updateData.username = data.fullname;
    }
    if (Object.keys(updateData).length > 0) {
        await axios.put(`${AUTH_SERVICE_URL}/users/${id}`, updateData, {
            headers: getAuthHeaders(token)
        });
    }
};

const generatePassword = (length: number = 12): string => {
    const chars =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+[]{}|;:,.<>?";
    let password = "";
    for (let i = 0; i < length; i++) {
        password += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return password;
};