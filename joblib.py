import joblib

# Save the best model
joblib.dump(rf, 'used_car_price_model.pkl')
print("Model saved successfully!")

# Optional: Save feature names for deployment
joblib.dump(list(X.columns), 'feature_names.pkl')
