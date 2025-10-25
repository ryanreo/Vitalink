package com.vitalink;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import java.util.Arrays;
import java.util.List;

public class MainActivity extends AppCompatActivity {

    private RecyclerView featuresRecyclerView;
    private FeaturesAdapter featuresAdapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        initializeViews();
        setupFeaturesRecyclerView();
        setupClickListeners();
    }

    private void initializeViews() {
        featuresRecyclerView = findViewById(R.id.featuresRecyclerView);
        Button btnGetStarted = findViewById(R.id.btnGetStarted);
        Button btnLearnMore = findViewById(R.id.btnLearnMore);
    }

    private void setupFeaturesRecyclerView() {
        List<Feature> features = Arrays.asList(
                new Feature("Video Consultations", "Face-to-face consultations with doctors", R.drawable.ic_video),
                new Feature("24/7 Availability", "Access healthcare professionals anytime", R.drawable.ic_clock),
                new Feature("Digital Prescriptions", "Get prescriptions delivered digitally", R.drawable.ic_prescription),
                new Feature("Secure & Private", "Enterprise-grade security for your data", R.drawable.ic_shield)
        );

        featuresAdapter = new FeaturesAdapter(features);
        featuresRecyclerView.setLayoutManager(new LinearLayoutManager(this));
        featuresRecyclerView.setAdapter(featuresAdapter);
    }

    private void setupClickListeners() {
        Button btnGetStarted = findViewById(R.id.btnGetStarted);
        Button btnLearnMore = findViewById(R.id.btnLearnMore);

        btnGetStarted.setOnClickListener(v -> {
            // Navigate to signup activity
            Intent intent = new Intent(MainActivity.this, SignupActivity.class);
            startActivity(intent);
        });

        btnLearnMore.setOnClickListener(v -> {
            // Scroll to features or show more info
            featuresRecyclerView.smoothScrollToPosition(0);
        });
    }
}