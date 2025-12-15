package com.wessim.authservice.service;

import com.wessim.authservice.entity.Role;
import com.wessim.authservice.entity.User;
import com.wessim.authservice.repository.UserRepo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.util.Pair;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.Map;

@Service
public class AuthService {

    @Autowired
    private UserRepo userRepo;

    public User register(String username, String email, String password, Role role) {
        User user = new User();
        user.setUsername(username);
        user.setEmail(email);
        user.setPasswordHash(new BCryptPasswordEncoder().encode(password));
        user.setRole(role);
        user.setActiveStatus(false);

        System.out.println("Registering user: " + username + ", email: " + email + ", role: " + role);
        return userRepo.save(user);
    }

    public User login(String username) {
        return userRepo.findByUsername(username);
    }

    public boolean checkPassword(String rawPassword, String storedHash) {
        return new BCryptPasswordEncoder().matches(rawPassword, storedHash);
    }

    public boolean deleteUserById(int id) {
        if (userRepo.existsById(id)) {
            userRepo.deleteById(id);
            return true;
        }
        return false;
    }

    public Pair<Boolean, String> updatePaymentStatus(Integer id) {
        User user = userRepo.findById(id).orElse(null);

        if (user == null) {
            return Pair.of(false, "User not found");
        }

        if (user.isActiveStatus()) {
            return Pair.of(false, "Payment already done");
        }

        user.setActiveStatus(true);
        userRepo.save(user);

        return Pair.of(true, "Payment processed successfully");
    }

}
