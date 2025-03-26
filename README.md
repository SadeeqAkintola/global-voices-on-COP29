# global-voices-on-COP29
# COP29 Twitter Sentiment Analysis

## Project Overview
This repository contains the implementation of Aspect-Based Sentiment Analysis (ABSA) on Twitter data collected during COP29. The project analyzes 180,000 tweets to understand public sentiment across various aspects of climate change discussions using GPT4-mini for efficient and accurate sentiment analysis.

## Requirements
```
python>=3.8
pytorch>=2.0.0
transformers>=4.30.0
openai>=0.28
pandas>=1.5.0
numpy>=1.23.0
matplotlib>=3.6.0
seaborn>=0.12.0
```

## Data Structure
The analysis uses three CSV files containing Twitter data:
```
data/
├── pre_cop29.csv        # Pre-COP29 tweets 
├── during_cop29.csv     # During-COP29 tweets 
└── post_cop29.csv       # Post-COP29 tweets 
```

## Project Structure
```
cop29-sentiment/
│
├── data/                # CSV files containing Twitter data
├── processed/           # Cleaned and preprocessed data
└── models/             # Model configuration and prompts
│
├── src/
│   ├── preprocessing/   # Data cleaning and preparation
│   ├── models/         # GPT4-mini integration
│   ├── analysis/       # ABSA implementation
│   └── visualization/  # Plotting and visualization tools
│
├── notebooks/          # Jupyter notebooks for analysis
├── results/           # Output visualizations and analysis
└── configs/          # Configuration files
```

## Key Features
1. Multi-aspect sentiment analysis covering:
   - Climate Action and Policy
   - Global Cooperation
   - Finance and Climate Justice
   - Technology and Innovation
   - Public Awareness
   - Adaptation and Resilience
   - Loss and Damage
   - Carbon Markets

2. Advanced NLP preprocessing pipeline:
   - Text cleaning and normalization
   - Language detection and filtering
   - Efficient batch processing

3. Zero-shot aspect detection and sentiment classification using GPT4-mini
4. Interactive visualizations and temporal analysis

## Quick Start
1. Clone the repository:
```bash
git clone https://github.com/Cop29Paper/Cop29-sentiment.git
cd cop29-sentiment
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure OpenAI API:
```bash
export OPENAI_API_KEY='your-api-key'
```

4. Verify data files:
   Ensure the following CSV files are present in the `data/` directory:
   - pre_cop29.csv 
   - during_cop29.csv 
   - post_cop29.csv 

5. Run the preprocessing pipeline:
```bash
python src/preprocessing/main.py --input_path data/raw --output_path data/processed
```

6. Execute the ABSA analysis:
```bash
python src/analysis/absa.py --data_path data/processed --output_path results
```

## Model Implementation
- **Core Model**: GPT4-mini for zero-shot aspect detection and sentiment analysis
- **Preprocessing**: Custom pipeline for Twitter text normalization
- **Prompting Strategy**: Engineered prompts for consistent ABSA outputs

### Key Advantages
1. Zero-shot capabilities eliminate need for fine-tuning
2. Efficient processing of large tweet volumes
3. Consistent aspect detection across the dataset
4. Robust handling of climate-specific terminology

## Results
The analysis reveals several key findings:
- Temporal shifts in sentiment across COP29 phases
- Regional variations in climate finance perception
- Strong correlation between policy announcements and public sentiment

## Visualization Examples
Key visualizations include:
- Sentiment distribution heatmaps
- Temporal trend analysis
- Geographic sentiment comparisons
- Aspect correlation matrices

## Contributing
We welcome contributions! Please follow these steps:
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Citation
If you use this code or dataset in your research, please cite:
```
@article{author2024cop29,
  title={Global Sentiments on Climate Action: A Twitter Analysis of COP29 Discussions},
  journal={Environmental Data Science},
  year={2024}
}
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- OpenAI for GPT4-mini model access
- Climate research community for valuable feedback

## Contact
For questions or feedback, please contact:
- Email: wole@readrly.io
- Twitter: @wolefizzy
