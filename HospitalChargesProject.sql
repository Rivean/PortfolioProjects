SELECT *
FROM HospitalCharges
ORDER BY Provider_State, DRG_Definition;

--Order the DRGs from most expensive to least expensive by state and provider
SELECT DRG_Definition, Provider_Name, Provider_State, Provider_id, Average_total_payments, Average_Medicare_Payments
FROM HospitalCharges
ORDER BY Provider_State, Provider_Name, Average_Total_Payments DESC;


--View how much hospitals in a state charge on average for a specific Diagnosis Related Group (DRG)
DECLARE @Code as varchar(max)
DECLARE @State as nchar(2)
--For @Code can change the number but must leave the "%" symbol there
SET @Code = '207%'
SET @State = 'TX'

SELECT DRG_Definition, Provider_Name, Provider_State, Provider_id, Average_total_payments, Average_Medicare_Payments
FROM HospitalCharges
WHERE DRG_Definition like @Code  AND Provider_State = @State
ORDER BY Average_Total_Payments DESC;


--The same as previous query, but with a user defined function instead
CREATE FUNCTION DrgStateCost(@code varchar(max), @State nchar(2))
RETURNS @DRGAvgStateCost TABLE(
DRG varchar(max), 
Provider varchar(max),
ProviderState nchar(2),
ProviderId int, 
AvgPayment money, 
AvgMedicarePayment money
) AS BEGIN INSERT INTO @DRGAvgStateCost
SELECT DRG_Definition, Provider_Name, Provider_State, Provider_id, Average_total_payments, Average_Medicare_Payments
FROM HospitalCharges
WHERE DRG_Definition like @Code  AND Provider_State = @State
ORDER BY Average_Total_Payments DESC
RETURN
END;

SELECT *
FROM dbo.DrgStateCost('192%', 'TX')
ORDER BY AvgPayment DESC;


-- Which hospitals charge the most for the same DRG?
DECLARE @DRGCode as varchar(max)

SET @DRGCode = '207%'

SELECT DRG_Definition, Provider_Name, Provider_State, Provider_id, Average_total_payments
FROM HospitalCharges
WHERE DRG_Definition like @DRGCode
ORDER BY Average_Total_Payments DESC


-- What is the avg cost for each DRG, and which hospitals are above or below avg cost?
DECLARE @DRGCode as varchar(max)

SET @DRGCode = '207%'

SELECT DRG_Definition, Provider_Name, Provider_State, Provider_id, Average_total_payments, Average_Medicare_Payments,
CASE
	WHEN Average_total_payments > AVG(Average_total_payments) over(PARTITION BY DRG_Definition) THEN 'Above Average'
	WHEN Average_total_payments < AVG(Average_total_payments) over(PARTITION BY DRG_Definition) THEN 'Below Average'
	WHEN Average_total_payments = AVG(Average_total_payments) over(PARTITION BY DRG_Definition) THEN 'Average'
	END AS DRGCost
FROM HospitalCharges
GROUP BY DRG_Definition, Provider_Name, Provider_State, Provider_id, Average_total_payments, Average_Medicare_Payments
HAVING DRG_Definition like @DRGCode
ORDER BY Provider_State

