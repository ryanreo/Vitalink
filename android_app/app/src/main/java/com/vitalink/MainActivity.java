package com.vitalink;

import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {

    private RecyclerView doctorsRecyclerView;
    private DoctorsAdapter doctorsAdapter;
    private List<Doctor> doctorList;
    private RequestQueue requestQueue;
    private TextView statusText;

    // Update this to your actual local IP if testing on emulator
    private final String BASE_URL = "http://10.0.2.2:5000/api"; // 10.0.2.2 is localhost for emulator

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        initializeViews();
        setupRecyclerView();
        setupClickListeners();

        // Initialize Volley request queue
        requestQueue = Volley.newRequestQueue(this);

        // Test API connection
        testApiConnection();

        // Load doctors
        loadDoctors();
    }

    private void initializeViews() {
        doctorsRecyclerView = findViewById(R.id.doctorsRecyclerView);
        statusText = findViewById(R.id.statusText);
        Button btnGetStarted = findViewById(R.id.btnGetStarted);
        Button btnLearnMore = findViewById(R.id.btnLearnMore);
    }

    private void setupRecyclerView() {
        doctorList = new ArrayList<>();
        doctorsAdapter = new DoctorsAdapter(doctorList);
        doctorsRecyclerView.setLayoutManager(new LinearLayoutManager(this));
        doctorsRecyclerView.setAdapter(doctorsAdapter);
    }

    private void setupClickListeners() {
        Button btnGetStarted = findViewById(R.id.btnGetStarted);
        Button btnLearnMore = findViewById(R.id.btnLearnMore);

        btnGetStarted.setOnClickListener(v -> {
            Toast.makeText(MainActivity.this, "Get Started Clicked!", Toast.LENGTH_SHORT).show();
            loadDoctors(); // Refresh doctors list
        });

        btnLearnMore.setOnClickListener(v -> {
            doctorsRecyclerView.smoothScrollToPosition(0);
        });
    }

    private void testApiConnection() {
        String url = BASE_URL.replace("/api", "") + "/api/health";

        JsonObjectRequest healthRequest = new JsonObjectRequest(
                Request.Method.GET,
                url,
                null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            String status = response.getString("status");
                            String dbStatus = response.getString("database");
                            statusText.setText("API Status: " + status + " | DB: " + dbStatus);
                        } catch (JSONException e) {
                            statusText.setText("API Connected - Parse Error");
                        }
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        statusText.setText("API Connection Failed");
                        Toast.makeText(MainActivity.this, "Cannot connect to backend", Toast.LENGTH_LONG).show();
                    }
                }
        );

        requestQueue.add(healthRequest);
    }

    private void loadDoctors() {
        String url = BASE_URL + "/doctors";

        JsonObjectRequest doctorsRequest = new JsonObjectRequest(
                Request.Method.GET,
                url,
                null,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            JSONArray doctorsArray = response.getJSONArray("doctors");
                            doctorList.clear();

                            for (int i = 0; i < doctorsArray.length(); i++) {
                                JSONObject doctorJson = doctorsArray.getJSONObject(i);
                                Doctor doctor = new Doctor(
                                        doctorJson.getInt("id"),
                                        doctorJson.getString("first_name"),
                                        doctorJson.getString("last_name"),
                                        doctorJson.getString("specialization"),
                                        doctorJson.getDouble("consultation_fee"),
                                        doctorJson.getBoolean("available"),
                                        doctorJson.getBoolean("is_online"),
                                        doctorJson.getDouble("avg_rating")
                                );
                                doctorList.add(doctor);
                            }

                            doctorsAdapter.notifyDataSetChanged();

                            if (doctorList.isEmpty()) {
                                statusText.setText("No doctors available");
                            } else {
                                statusText.setText("Found " + doctorList.size() + " doctors");
                            }

                        } catch (JSONException e) {
                            statusText.setText("Error parsing doctors data");
                            Toast.makeText(MainActivity.this, "Error loading doctors", Toast.LENGTH_SHORT).show();
                        }
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        statusText.setText("Failed to load doctors");
                        Toast.makeText(MainActivity.this, "Error: " + error.getMessage(), Toast.LENGTH_LONG).show();
                    }
                }
        );

        requestQueue.add(doctorsRequest);
    }
}