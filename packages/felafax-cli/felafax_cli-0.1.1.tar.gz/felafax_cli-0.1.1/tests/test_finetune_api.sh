#!/bin/bash

# Configuration
SERVER="http://localhost:8000"
USER_ID="b4c9a289323b"
DATASET_ID="dataset_86c1dd476e63"

# Function definitions
start_finetune() {
    echo "📋 Starting fine-tune job..."
    START_RESPONSE=$(curl -s -X POST \
        "${SERVER}/fine-tune/${USER_ID}/start" \
        -H 'Content-Type: application/json' \
        -d '{
            "dataset_id": "'${DATASET_ID}'",
            "model_name": "llama3-8b",
            "config": {
                "learning_rate": 1e-5,
                "num_epochs": 3,
                "batch_size": 4,
                "warmup_steps": 100
            }
        }')
    
    JOB_ID=$(echo $START_RESPONSE | grep -o '"tune_id":"[^"]*' | cut -d'"' -f4)
    echo "✅ Fine-tune job started. Job ID: ${JOB_ID}"
    echo $JOB_ID  # Return job ID for other functions
}

check_status() {
    local job_id=$1
    echo "📊 Checking job status..."
    curl -s -X GET \
        "${SERVER}/fine-tune/${USER_ID}/${job_id}/status" \
        -H 'accept: application/json' | jq '.'
}

stop_finetune() {
    local job_id=$1
    echo "🛑 Stopping fine-tune job..."
    curl -s -X POST \
        "${SERVER}/fine-tune/${USER_ID}/${job_id}/stop" \
        -H 'accept: application/json' | jq '.'
}

run_full_test() {
    echo "🚀 Running full fine-tune API test"
    echo "------------------------"

    # Start and get job ID
    JOB_ID=$(start_finetune)
    echo

    # Initial status check
    check_status $JOB_ID
    echo

    # Wait and check again
    echo "⏳ Waiting for 5 seconds..."
    sleep 5
    check_status $JOB_ID
    echo

    # Stop job
    stop_finetune $JOB_ID
    echo

    # Final status check
    check_status $JOB_ID
    echo

    echo "✨ All operations completed!"
}

# Command handling
case "$1" in
    "start")
        start_finetune
        ;;
    "status")
        if [ -z "$2" ]; then
            echo "Error: Job ID required for status check"
            exit 1
        fi
        check_status $2
        ;;
    "stop")
        if [ -z "$2" ]; then
            echo "Error: Job ID required for stop command"
            exit 1
        fi
        stop_finetune $2
        ;;
    *)
        run_full_test
        ;;
esac

