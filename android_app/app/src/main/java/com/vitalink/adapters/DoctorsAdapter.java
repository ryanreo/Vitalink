package com.vitalink.adapters;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import com.vitalink.models.Doctor;
import com.vitalink.R;
import java.util.List;

public class DoctorsAdapter extends RecyclerView.Adapter<DoctorsAdapter.DoctorViewHolder> {

    private List<Doctor> doctorList;

    public DoctorsAdapter(List<Doctor> doctorList) {
        this.doctorList = doctorList;
    }

    @NonNull
    @Override
    public DoctorViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_doctor, parent, false);
        return new DoctorViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull DoctorViewHolder holder, int position) {
        Doctor doctor = doctorList.get(position);
        holder.bind(doctor);
    }

    @Override
    public int getItemCount() {
        return doctorList.size();
    }

    static class DoctorViewHolder extends RecyclerView.ViewHolder {
        private TextView doctorName;
        private TextView specialization;
        private TextView fee;
        private TextView status;
        private TextView rating;

        public DoctorViewHolder(@NonNull View itemView) {
            super(itemView);
            doctorName = itemView.findViewById(R.id.doctorName);
            specialization = itemView.findViewById(R.id.specialization);
            fee = itemView.findViewById(R.id.consultationFee);
            status = itemView.findViewById(R.id.status);
            rating = itemView.findViewById(R.id.rating);
        }

        public void bind(Doctor doctor) {
            doctorName.setText(doctor.getFullName());
            specialization.setText(doctor.getSpecialization());
            fee.setText("$" + doctor.getConsultationFee());
            rating.setText("⭐ " + doctor.getRating());

            if (doctor.isOnline()) {
                status.setText("🟢 Online");
                status.setTextColor(itemView.getContext().getColor(android.R.color.holo_green_dark));
            } else {
                status.setText("⚫ Offline");
                status.setTextColor(itemView.getContext().getColor(android.R.color.darker_gray));
            }
        }
    }
}