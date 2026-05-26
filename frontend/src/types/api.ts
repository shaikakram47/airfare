export interface FlightInput {
  airline: string;
  source_city: string;
  destination_city: string;
  departure_time: string;
  arrival_time: string;
  stops: string;
  class: string;
  duration: number;
  days_left: number;
}

export interface PredictionSummary {
  input: FlightInput;
  predicted_fare: number;
  currency: string;
}

export interface ModelMetric {
  model_name: string;
  rmse: number;
  mae: number;
  r2: number;
  is_best: boolean;
}

export interface FormOptions {
  airlines: string[];
  cities: string[];
  time_buckets: string[];
  stops: string[];
  classes: string[];
}

export interface TrainResponse {
  message: string;
  best_model: string;
  training_samples: number;
  metrics: ModelMetric[];
}
