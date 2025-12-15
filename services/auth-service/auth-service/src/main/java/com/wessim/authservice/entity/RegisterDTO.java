package com.wessim.authservice.entity;


import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
public class RegisterDTO {
    private String username;
    private String email;
    private String password;
    private Role role;
    private
    public RegisterDTO() {
    }

    public RegisterDTO(String username, String email, String password, Role role) {
        this.username = username;
        this.email = email;
        this.password = password;
        this.role = role;
    }


}
