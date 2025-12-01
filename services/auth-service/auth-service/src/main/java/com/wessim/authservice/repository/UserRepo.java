package com.wessim.authservice.repository;

import com.wessim.authservice.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface UserRepo extends JpaRepository<User, Integer> {
    User findByEmail(String email);
    User findByUsername(String username);
}
