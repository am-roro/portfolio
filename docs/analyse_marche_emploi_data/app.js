// Attendre le chargement complet du DOM
document.addEventListener("DOMContentLoaded", () => {
    if (typeof MARKET_DATA === "undefined" || !MARKET_DATA.jobs) {
        console.error("Données MARKET_DATA non trouvées. Veuillez exécuter analyze.py d'abord.");
        return;
    }

    const jobs = MARKET_DATA.jobs;

    // Références DOM
    const filterRole = document.getElementById("filter-role");
    const filterCity = document.getElementById("filter-city");
    const filterContract = document.getElementById("filter-contract");
    const btnReset = document.getElementById("btn-reset");
    const tableBody = document.getElementById("jobs-table-body");

    // Éléments KPI
    const kpiTotalJobs = document.getElementById("kpi-total-jobs");
    const kpiAvgSalary = document.getElementById("kpi-avg-salary");
    const kpiTopSkill = document.getElementById("kpi-top-skill");
    const kpiRatio = document.getElementById("kpi-ratio");

    // Instances globales des graphiques Chart.js (pour pouvoir les détruire/recréer lors des filtres)
    let chartSkills = null;
    let chartContracts = null;
    let chartSalaries = null;
    let chartCities = null;

    // 1. Initialiser et peupler les listes déroulantes de filtres
    initFilters();

    // 2. Premier rendu du dashboard avec toutes les offres
    updateDashboard(jobs);

    // 3. Écouteurs d'événements pour les filtres
    filterRole.addEventListener("change", applyFilters);
    filterCity.addEventListener("change", applyFilters);
    filterContract.addEventListener("change", applyFilters);
    
    btnReset.addEventListener("click", () => {
        filterRole.value = "all";
        filterCity.value = "all";
        filterContract.value = "all";
        updateDashboard(jobs);
    });

    // --- FONCTIONS ---

    function initFilters() {
        // Extraire les valeurs uniques
        const roles = [...new Set(jobs.map(j => j.title))].sort();
        const cities = [...new Set(jobs.map(j => j.location))].sort();
        const contracts = [...new Set(jobs.map(j => j.contract))].sort();

        // Remplir le filtre Métiers
        roles.forEach(role => {
            const opt = document.createElement("option");
            opt.value = role;
            opt.textContent = role;
            filterRole.appendChild(opt);
        });

        // Remplir le filtre Villes
        cities.forEach(city => {
            const opt = document.createElement("option");
            opt.value = city;
            opt.textContent = city;
            filterCity.appendChild(opt);
        });

        // Remplir le filtre Contrats
        contracts.forEach(contract => {
            const opt = document.createElement("option");
            opt.value = contract;
            opt.textContent = contract;
            filterContract.appendChild(opt);
        });
    }

    function applyFilters() {
        const selectedRole = filterRole.value;
        const selectedCity = filterCity.value;
        const selectedContract = filterContract.value;

        let filteredJobs = jobs;

        if (selectedRole !== "all") {
            filteredJobs = filteredJobs.filter(j => j.title === selectedRole);
        }
        if (selectedCity !== "all") {
            filteredJobs = filteredJobs.filter(j => j.location === selectedCity);
        }
        if (selectedContract !== "all") {
            filteredJobs = filteredJobs.filter(j => j.contract === selectedContract);
        }

        updateDashboard(filteredJobs);
    }

    function updateDashboard(filteredJobs) {
        // A. Mettre à jour les KPIs
        updateKPIs(filteredJobs);

        // B. Mettre à jour les graphiques
        renderChartSkills(filteredJobs);
        renderChartContracts(filteredJobs);
        renderChartSalaries(filteredJobs);
        renderChartCities(filteredJobs);

        // C. Mettre à jour le tableau
        renderTable(filteredJobs);
    }

    function updateKPIs(filteredJobs) {
        // Total d'offres
        kpiTotalJobs.textContent = filteredJobs.length.toLocaleString();

        // Salaire moyen (exclure Alternances et Stages pour ne pas fausser)
        const salaryJobs = filteredJobs.filter(j => 
            j.salary_annual_eur && 
            j.salary_annual_eur > 0 && 
            !["Alternance", "Stage"].includes(j.contract)
        );
        if (salaryJobs.length > 0) {
            const sum = salaryJobs.reduce((acc, curr) => acc + curr.salary_annual_eur, 0);
            const avg = Math.round(sum / salaryJobs.length);
            kpiAvgSalary.textContent = `${avg.toLocaleString()} €`;
        } else {
            kpiAvgSalary.textContent = "N/A";
        }

        // Compétence reine
        const allSkills = filteredJobs.flatMap(j => j.skills_list);
        if (allSkills.length > 0) {
            const skillCounts = {};
            allSkills.forEach(s => skillCounts[s] = (skillCounts[s] || 0) + 1);
            const sortedSkills = Object.entries(skillCounts).sort((a, b) => b[1] - a[1]);
            kpiTopSkill.textContent = sortedSkills[0][0];
        } else {
            kpiTopSkill.textContent = "N/A";
        }

        // Part Alternance + Stages
        const altOrStageJobs = filteredJobs.filter(j => ["Alternance", "Stage"].includes(j.contract));
        if (filteredJobs.length > 0) {
            const ratio = Math.round((altOrStageJobs.length / filteredJobs.length) * 100);
            kpiRatio.textContent = `${ratio}%`;
        } else {
            kpiRatio.textContent = "0%";
        }
    }

    function renderChartSkills(filteredJobs) {
        if (chartSkills) chartSkills.destroy();

        const ctx = document.getElementById("chart-top-skills").getContext("2d");
        
        // Calculer la fréquence
        const allSkills = filteredJobs.flatMap(j => j.skills_list);
        const skillCounts = {};
        allSkills.forEach(s => skillCounts[s] = (skillCounts[s] || 0) + 1);
        const sortedSkills = Object.entries(skillCounts)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 10); // Top 10

        const labels = sortedSkills.map(s => s[0]);
        const counts = sortedSkills.map(s => s[1]);

        // Dégradé de couleur
        const gradient = ctx.createLinearGradient(0, 0, 400, 0);
        gradient.addColorStop(0, '#6366f1'); // Indigo
        gradient.addColorStop(1, '#a855f7'); // Violet purple

        chartSkills = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Nombre de requêtes',
                    data: counts,
                    backgroundColor: gradient,
                    borderColor: 'rgba(255, 255, 255, 0.1)',
                    borderWidth: 1,
                    borderRadius: 8,
                    barThickness: 16
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: '#111029',
                        titleColor: '#fff',
                        bodyColor: '#e2e8f0',
                        borderColor: 'rgba(255,255,255,0.1)',
                        borderWidth: 1
                    }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#9ca3af' }
                    },
                    y: {
                        grid: { display: false },
                        ticks: { color: '#f3f4f6', font: { weight: 500 } }
                    }
                }
            }
        });
    }

    function renderChartContracts(filteredJobs) {
        if (chartContracts) chartContracts.destroy();

        const ctx = document.getElementById("chart-contracts").getContext("2d");

        // Compter les contrats
        const contractCounts = {};
        filteredJobs.forEach(j => {
            contractCounts[j.contract] = (contractCounts[j.contract] || 0) + 1;
        });

        const labels = Object.keys(contractCounts);
        const counts = Object.values(contractCounts);

        chartContracts = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: counts,
                    backgroundColor: [
                        '#6366f1', // CDI (Indigo)
                        '#fbbf24', // Alternance (Amber)
                        '#f472b6', // Freelance (Rose)
                        '#2dd4bf', // CDD (Teal)
                        '#34d399'  // Stage (Emerald)
                    ],
                    borderWidth: 2,
                    borderColor: '#120d2d',
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            color: '#9ca3af',
                            font: { size: 11 },
                            padding: 15
                        }
                    },
                    tooltip: {
                        backgroundColor: '#111029',
                        titleColor: '#fff',
                        bodyColor: '#e2e8f0',
                        borderColor: 'rgba(255,255,255,0.1)',
                        borderWidth: 1
                    }
                },
                cutout: '65%'
            }
        });
    }

    function renderChartSalaries(filteredJobs) {
        if (chartSalaries) chartSalaries.destroy();

        const ctx = document.getElementById("chart-salary-role").getContext("2d");

        // Exclure alternances et stages
        const cdiFreelance = filteredJobs.filter(j => 
            j.salary_annual_eur && 
            j.salary_annual_eur > 0 && 
            !["Alternance", "Stage"].includes(j.contract)
        );

        // Grouper par rôle
        const roleSalaries = {};
        cdiFreelance.forEach(j => {
            if (!roleSalaries[j.title]) roleSalaries[j.title] = [];
            roleSalaries[j.title].push(j.salary_annual_eur);
        });

        const labels = Object.keys(roleSalaries);
        const averages = labels.map(role => {
            const arr = roleSalaries[role];
            return Math.round(arr.reduce((a, b) => a + b, 0) / arr.length);
        });

        // Dégradé turquoise
        const gradient = ctx.createLinearGradient(0, 0, 0, 250);
        gradient.addColorStop(0, '#14b8a6');
        gradient.addColorStop(1, '#0f766e');

        chartSalaries = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Salaire moyen (€ brute/an)',
                    data: averages,
                    backgroundColor: gradient,
                    borderColor: 'rgba(255,255,255,0.1)',
                    borderWidth: 1,
                    borderRadius: 6,
                    barThickness: 24
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: '#111029',
                        callbacks: {
                            label: function(context) {
                                return ` ${context.parsed.y.toLocaleString()} € / an`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: '#f3f4f6' }
                    },
                    y: {
                        grid: { color: 'rgba(255,255,255,0.05)' },
                        ticks: {
                            color: '#9ca3af',
                            callback: function(value) {
                                return (value / 1000) + 'k €';
                            }
                        }
                    }
                }
            }
        });
    }

    function renderChartCities(filteredJobs) {
        if (chartCities) chartCities.destroy();

        const ctx = document.getElementById("chart-cities").getContext("2d");

        // Compter par ville
        const cityCounts = {};
        filteredJobs.forEach(j => {
            cityCounts[j.location] = (cityCounts[j.location] || 0) + 1;
        });

        // Trier par nombre et prendre les 6 premières
        const sortedCities = Object.entries(cityCounts)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 6);

        const labels = sortedCities.map(c => c[0]);
        const counts = sortedCities.map(c => c[1]);

        chartCities = new Chart(ctx, {
            type: 'polarArea',
            data: {
                labels: labels,
                datasets: [{
                    data: counts,
                    backgroundColor: [
                        'rgba(99, 102, 241, 0.65)',  // Indigo
                        'rgba(20, 184, 166, 0.65)',  // Teal
                        'rgba(217, 70, 239, 0.65)',  // Rose
                        'rgba(245, 158, 11, 0.65)',   // Amber
                        'rgba(16, 185, 129, 0.65)',  // Emerald
                        'rgba(59, 130, 246, 0.65)'   // Blue
                    ],
                    borderColor: 'rgba(255, 255, 255, 0.1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { display: false },
                        angleLines: { color: 'rgba(255, 255, 255, 0.05)' }
                    }
                },
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#9ca3af',
                            font: { size: 10 },
                            boxWidth: 12,
                            padding: 8
                        }
                    },
                    tooltip: {
                        backgroundColor: '#111029',
                        titleColor: '#fff',
                        bodyColor: '#e2e8f0',
                        borderColor: 'rgba(255,255,255,0.1)',
                        borderWidth: 1
                    }
                }
            }
        });
    }

    function renderTable(filteredJobs) {
        tableBody.innerHTML = "";

        // Trier par date décroissante et prendre les 8 premiers
        const sortedJobs = [...filteredJobs]
            .sort((a, b) => new Date(b.date_posted) - new Date(a.date_posted))
            .slice(0, 8);

        if (sortedJobs.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--text-secondary); padding: 2rem;">Aucune offre ne correspond aux critères sélectionnés.</td></tr>`;
            return;
        }

        sortedJobs.forEach(job => {
            const tr = document.createElement("tr");

            // Déterminer la classe de badge de contrat
            let contractClass = "contract-cdi";
            if (job.contract === "Alternance") contractClass = "contract-alternance";
            else if (job.contract === "Freelance") contractClass = "contract-freelance";
            else if (job.contract === "CDD") contractClass = "contract-cdd";
            else if (job.contract === "Stage") contractClass = "contract-stage";

            // Formater la date en Français
            const dateParts = job.date_posted.split("-");
            const formattedDate = dateParts.length === 3 ? `${dateParts[2]}/${dateParts[1]}` : job.date_posted;

            tr.innerHTML = `
                <td style="font-weight: 600;">${job.title}</td>
                <td>${job.company}</td>
                <td><span style="display: flex; align-items: center; gap: 0.25rem;">📍 ${job.location}</span></td>
                <td><span class="badge-contract ${contractClass}">${job.contract}</span></td>
                <td style="font-family: monospace; color: #2dd4bf; font-weight: 500;">${job.salary_raw}</td>
                <td style="color: var(--text-secondary); font-size: 0.8rem;">${formattedDate}</td>
            `;

            tableBody.appendChild(tr);
        });
    }
});
