from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Choose a model that has severity/priority-like labels
model_name = "CIRCL/vulnerability-severity-classification-roberta-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

labels = ["low", "medium", "high", "critical"]
# Function to predict priority/severity from input text
def predict_priority(text):
    # Tokenize the input text for the model
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    # Disable gradient calculation for inference
    with torch.no_grad():
        # Get model outputs (logits)
        outputs = model(**inputs)
        # Convert logits to probabilities using softmax
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    # Find the index of the highest probability
    max_idx = torch.argmax(probs, dim=-1).item()
    # Return the label and its confidence score
    return labels[max_idx], probs[0][max_idx].item()

# Example
complaint = "The street light near my house is flickering."
priority, confidence = predict_priority(complaint)
print( priority)