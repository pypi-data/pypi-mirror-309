# ORruns: Redefining Operations Research Experiment Management 🚀

<p align="center">
  <img src="orruns/assets/logo.png" alt="ORruns Logo" width="200"/>
  <br>
  <em>Next-generation Experiment Management Platform for Operations Research</em>
</p>

> 🌱 ORruns is in its vibrant early stages. As a newly launched open-source project, we welcome every Operations Research researcher to participate and contribute. Your ideas and code will help this project grow better. Let's build the future of the Operations Research community together!

<p align="center">
  <a href="#quick-start">Quick Start</a> •
  <a href="#why-orruns">Why ORruns</a> •
  <a href="#community">Community</a> •
  <a href="#features">Features</a>
</p>

---

## Why ORruns?

Have you encountered these challenges in Operations Research?

- 📊 Experimental data scattered everywhere, difficult to manage and track
- 🔄 Tedious experiment repetition and chaotic parameter management
- 📈 Repetitive code writing for visualization
- 🤝 Lack of unified experiment management and sharing platform

**ORruns** is born to solve these problems! We are committed to providing Operations Research researchers with a modern, intuitive, and powerful experiment management tool.

## ✨ Features

### Elegant Experiment Tracking

#### Simple Single-Run Experiment 
```python
@repeat_experiment(times=1)
def optimize_with_different_seeds(tracker):
    tracker.log_params({
        "epoches": 1000
    })
    # Your optimization code
    result = optimize()
    # Automatic parallelization, result collection and visualization
    return your_optimization_algorithm()
```

#### Powerful Parallel Experiment Support
```python
@repeat_experiment(times=10, parallel=True)
def optimize_with_different_seeds(tracker):
    tracker.log_params({
        "population_size": 100,
        "generations": 1000
    })
    
    # Your optimization code
    result = optimize()
    
    tracker.log_metrics({
        "pareto_front_size": len(result.pareto_front),
        "hypervolume": result.hypervolume
    })
    # save the Pareto front Visualization
    tracker.log_artifact("pareto_front.png", plt.gcf())
    # Automatic parallelization, result collection and visualization
    return your_optimization_algorithm()
```

### Intuitive Visualization Interface
<p align="center">
  <img src="orruns/assets/web.png" alt="Dashboard Screenshot" width="600"/>
</p>

## 🚀 Quick Start

```bash
pip install orruns
```

Check out our [Quick Start Guide](https://orruns.readthedocs.io) to begin your first experiment!



## 🚀 Making Operations Research Better

We believe that the Operations Research community deserves modern and open tooling ecosystems like those in the machine learning community. ORruns is not just a tool, but a vision - let's together:

- 🌟 Build an open, active Operations Research community
- 🔧 Create better experiment management tools
- 📚 Share knowledge and best practices
- 🤝 Promote academic exchange and collaboration

## 💡 Join the Journey

> "The future of Operations Research needs our collective effort. Let's build an open-source community for Operations Research researchers!"

### 🌱 Growing Together from Zero

ORruns is still a young project, which means:
- You can participate in core feature design and development
- Your ideas and suggestions are more likely to be adopted
- You can witness and influence every step of the project's growth
- You'll be among the earliest contributors

### 💪 How to Contribute

Whether you are:
- 🎓 A student new to Operations Research
- 👨‍🔬 An experienced researcher
- 👩‍💻 A passionate developer
- 📚 An enthusiastic documentation writer

We welcome your participation:

- 🎯 **Use and Feedback**: Every suggestion drives ORruns to become better
- 🛠️ **Development**: Whether fixing bugs or adding features, all contributions are welcome
- 📝 **Documentation**: Help others understand and use ORruns
- 🌍 **Promotion**: Spread the word to more Operations Research researchers

## 🎯 Roadmap

We're planning exciting features to build a more comprehensive Operations Research experiment ecosystem:

### Coming Soon
- 📊 **Enhanced Analytics** (v0.2.0)
  - Dynamic Pareto Front Visualization
  - Advanced Statistical Analysis Tools
  - Experiment Comparison System

- 🛠️ **Improved User Experience** (v0.3.0)
  - Experiment Backup and Recovery
  - Publication-Ready Results Export
  - Powerful Command Line Tools

> Check out the complete [roadmap document](ROADMAP.md) for more details and future plans!


## 📄 License

ORruns is licensed under the GNU General Public License v3.0 (GPL-3.0) with additional non-commercial terms. This means: if you need to use this software for commercial purposes, please contact the project maintainers for a commercial license.
See the full license text in the [LICENSE](LICENSE) file.


## ☕ Support the Project
---
<a href="https://www.buymeacoffee.com/your_username" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>


## 🌟 Join the Community

- 💬 [Join Discussions](https://github.com/lengff123/ORruns/discussions)
- 🐛 [Report Issues](https://github.com/lengff123/ORruns/issues)
- 📫 [Mailing List](mailto:your-email@example.com)




<p align="center">
  <em>By Operations Researchers, For Operations Researchers</em>
  <br>
  <br>
  If you like this project, please give us a ⭐️
</p>

