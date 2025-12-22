package com.wessim.authservice.security;

import com.wessim.authservice.entity.User;
import com.wessim.authservice.repository.UserRepo;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

@Service
public class CustomUserDetailsService implements UserDetailsService {

    private final UserRepo userRepository;

    public CustomUserDetailsService(UserRepo userRepository) {
        this.userRepository = userRepository;
    }

    @Override
    public UserDetails loadUserByUsername(String username) {
        User user = userRepository.findByUsername(username); // returns User or null
        if (user == null) {
            throw new UsernameNotFoundException("User not found");
        }
        return user;
    }
}
