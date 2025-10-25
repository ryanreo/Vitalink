package com.vitalink.models;

public class Doctor {
    private int id;
    private String firstName;
    private String lastName;
    private String specialization;
    private double consultationFee;
    private boolean available;
    private boolean isOnline;
    private double rating;

    public Doctor(int id, String firstName, String lastName, String specialization,
                  double consultationFee, boolean available, boolean isOnline, double rating) {
        this.id = id;
        this.firstName = firstName;
        this.lastName = lastName;
        this.specialization = specialization;
        this.consultationFee = consultationFee;
        this.available = available;
        this.isOnline = isOnline;
        this.rating = rating;
    }

    // Getters
    public int getId() { return id; }
    public String getFirstName() { return firstName; }
    public String getLastName() { return lastName; }
    public String getFullName() { return firstName + " " + lastName; }
    public String getSpecialization() { return specialization; }
    public double getConsultationFee() { return consultationFee; }
    public boolean isAvailable() { return available; }
    public boolean isOnline() { return isOnline; }
    public double getRating() { return rating; }
}