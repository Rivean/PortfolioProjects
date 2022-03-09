--Make sure data was imported correctly 
SELECT *
FROM CovidPortfolioProject.dbo.CovidDeaths
ORDER BY 3, 4;

SELECT *
FROM CovidPortfolioProject.dbo.CovidVaccinations
ORDER BY 3, 4;

-- Select the data that I want to look at 
SELECT location, date, total_cases, new_cases, total_deaths, population
FROM CovidPortfolioProject.dbo.CovidDeaths
WHERE continent IS NOT NULL
ORDER BY 1, 2;

--Total Cases VS Total Deaths
SELECT location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 AS DeathPercentage
FROM CovidPortfolioProject.dbo.CovidDeaths
WHERE location LIKE '%States%'
ORDER BY 2;

--total cases vs population
SELECT location, date, total_cases, population, (total_cases/population)*100 AS PercentPopulationInfected
FROM CovidPortfolioProject.dbo.CovidDeaths
WHERE location LIKE '%States%'
ORDER BY 2;

--Highest infection percentage by population
SELECT location, population, MAX(total_cases) AS HighestInfectionCount, MAX((total_cases/population))*100 AS HighestInfectionPercentage
FROM CovidPortfolioProject.dbo.CovidDeaths
GROUP BY location, population
ORDER BY HighestInfectionPercentage DESC;

--Highest mortality by country
SELECT location, MAX(CAST(total_deaths as int)) AS TotalDeathCount
FROM CovidPortfolioProject.dbo.CovidDeaths
WHERE continent IS NOT NULL -- Needed as it will show continents without this part 
GROUP BY location
ORDER BY TotalDeathCount DESC;


/* BY CONTINENTS */

-- Highest death count by continent 
SELECT location, MAX(CAST(total_deaths as int)) AS TotalDeathCount
FROM CovidPortfolioProject.dbo.CovidDeaths
WHERE continent IS NULL
GROUP BY location 
ORDER BY TotalDeathCount DESC;


-- Global mortality 
SELECT SUM(new_cases) AS TotalCases, SUM(CAST(new_deaths as int)) AS TotalDeaths, SUM(CAST(new_deaths as int))/SUM(new_cases)*100 AS DeathPercentage 
FROM CovidPortfolioProject.dbo.CovidDeaths
WHERE continent IS NOT NULL
ORDER BY 1,2;


/* VACCINATIONS */

--Joining the two tables
SELECT *
FROM CovidPortfolioProject.dbo.CovidDeaths Death
JOIN CovidPortfolioProject.dbo.CovidVaccinations Vacc
	ON Death.location = Vacc.location
	AND Death.date = Vacc.date; 

--Total population vs vaccinations
SELECT Death.continent, Death.location, Death.date, Death.population, Vacc.new_vaccinations,
SUM(CAST(Vacc.new_vaccinations as int)) OVER (Partition by Death.location ORDER BY Death.location, Death.date) AS total_vaccinations_given
FROM CovidPortfolioProject.dbo.CovidDeaths Death
JOIN CovidPortfolioProject.dbo.CovidVaccinations Vacc
	ON Death.location = Vacc.location
	AND Death.date = Vacc.date 
WHERE Death.continent IS NOT NULL 
ORDER BY 2,3;


--Using CTE to find percentage of population vaccinated
WITH PopulationVacc AS (
SELECT Death.continent, Death.location, Death.date, Death.population, Vacc.new_vaccinations,
SUM(CAST(Vacc.new_vaccinations as int)) OVER (Partition by Death.location ORDER BY Death.location, Death.date) AS total_vaccinations_given
FROM CovidPortfolioProject.dbo.CovidDeaths Death
JOIN CovidPortfolioProject.dbo.CovidVaccinations Vacc
	ON Death.location = Vacc.location
	AND Death.date = Vacc.date 
WHERE Death.continent IS NOT NULL 
);
SELECT *, (total_vaccinations_given/population)*100 AS PercentagePopVaccinated 
FROM PopulationVacc;

-- Using a Temp Table instead of CTE 

DROP TABLE IF exists #PercentPopulationVaccinated 
CREATE TABLE #PercentPopulationVaccinated 
(
Continent nvarchar(255), 
Location nvarchar (255),
Date datetime,
Population numeric,
New_vaccinations numeric,
total_vaccinations_given numeric
);

INSERT INTO #PercentPopulationVaccinated 
SELECT Death.continent, Death.location, Death.date, Death.population, Vacc.new_vaccinations,
SUM(CAST(Vacc.new_vaccinations as int)) OVER (Partition by Death.location ORDER BY Death.location, Death.date) AS total_vaccinations_given
FROM CovidPortfolioProject.dbo.CovidDeaths Death
JOIN CovidPortfolioProject.dbo.CovidVaccinations Vacc
	ON Death.location = Vacc.location
	AND Death.date = Vacc.date 
WHERE Death.continent IS NOT NULL;

SELECT *, (total_vaccinations_given/population)*100 AS PercentagePopVaccinated 
FROM #PercentPopulationVaccinated; 


-- Creating view to store data for future visualizations 
CREATE VIEW PercentPopulationVaccinated AS
SELECT Death.continent, Death.location, Death.date, Death.population, Vacc.new_vaccinations,
SUM(CAST(Vacc.new_vaccinations as int)) OVER (Partition by Death.location ORDER BY Death.location, Death.date) AS total_vaccinations_given
FROM CovidPortfolioProject.dbo.CovidDeaths Death
JOIN CovidPortfolioProject.dbo.CovidVaccinations Vacc
	ON Death.location = Vacc.location
	AND Death.date = Vacc.date 
WHERE Death.continent IS NOT NULL;


-- Taking a holistic view of the USA including hospitalizations using CTE 
WITH USAStats AS(
SELECT Death.location, Death.date, Death.population, Death.total_cases, Death.total_deaths, (Death.total_deaths/Death.total_cases)*100 AS DeathPercentage,
Death.hosp_patients, Death.icu_patients, Vacc.new_vaccinations,
SUM(CAST(Vacc.new_vaccinations as int)) OVER (Partition by Death.location ORDER BY Death.location, Death.date) AS total_vaccinations_given
FROM CovidPortfolioProject.dbo.CovidDeaths Death
JOIN CovidPortfolioProject.dbo.CovidVaccinations Vacc
	ON Death.location = Vacc.location
	AND Death.date = Vacc.date 
WHERE Death.location LIKE '%States%'
);
SELECT*, (total_vaccinations_given/population)*100 AS PercentagePopVaccinated
FROM USAStats;
