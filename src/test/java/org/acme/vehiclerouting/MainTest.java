package org.acme.vehiclerouting;

import ai.timefold.solver.core.api.solver.Solver;
import ai.timefold.solver.core.api.solver.SolverFactory;
import org.acme.vehiclerouting.domain.*;
import org.junit.jupiter.api.Test;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.Duration;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.databind.ObjectMapper;

public class MainTest {

    private static final Logger LOGGER = LoggerFactory.getLogger(MainTest.class);

    @Test
    void test000() throws IOException {
        executeTest("/cvrptw-25customers.json");
    }

    void executeTest(String fileName) throws IOException {

        InputFileData inputFileData = FileReaderExample("C101.100.txt");

        List<Depot> depotList = new ArrayList<>();
        Depot depot = inputFileData.depot;
        depotList.add(depot);

        LocalDateTime iniTime = getTime(0);

        List<Vehicle> vehicleList = new ArrayList<>();
        for (int i = 0; i < inputFileData.nrVehicles; i++) {
            LocalDateTime departureTime = iniTime.plusSeconds(0);
            vehicleList.add(new Vehicle("veh-" + i, depot, departureTime));
        }

        List<Customer> customerList = inputFileData.customersList;

        Location southWestCorner = new Location(0, 0);
        Location northEastCorner = new Location(0, 0);

        VehicleRoutePlan problem = new VehicleRoutePlan(
                "problem",
                depotList,
                vehicleList,
                customerList,
                southWestCorner,
                northEastCorner,
                inputFileData.startDateTime,
                inputFileData.endDateTime
        );

        SolverFactory<VehicleRoutePlan> solverFactory = SolverFactory.createFromXmlResource(
                "solverConfig.xml");

        Solver<VehicleRoutePlan> solver = solverFactory.buildSolver();


        VehicleRoutePlan solution = solver.solve(problem);

        printSolution(solution);

    }

    public void printSolution(VehicleRoutePlan solution) {

        List<Vehicle> vehicleList = solution.getVehicles();
        List<Customer> customerList = solution.getCustomers();

        for (Customer customer : customerList) {
            if (customer.isServiceFinishedAfterDueTime()) {
                LOGGER.info("customer: " + customer.getId() + " delay: " + customer.getServiceFinishedDelayInMinutes());
            }
        }

        long totalDrivingTime = 0;
        for (Vehicle vehicle : vehicleList) {
            LOGGER.info("Vehicle: " + vehicle.getId());
            List<Customer> vehCustomerList = vehicle.getCustomers();
            for (Customer customer : vehCustomerList) {
                LOGGER.info("\tcustomer: " + customer);
            }
            if (vehCustomerList.size() > 0) {
                Customer lastCustomer = vehCustomerList.get(vehCustomerList.size()-1);
                long drivingTimeToDepot = lastCustomer.getLocation().getDrivingTimeTo(vehicle.getDepot().getLocation());
                long arrival =  Duration.between(vehicle.getDepartureTime(), lastCustomer.getDepartureTime()).toSeconds() + drivingTimeToDepot;
                LOGGER.info("Time of route: " + String.valueOf(arrival));
                totalDrivingTime += arrival;
            }

        }
        LOGGER.info("Total Driving Time: " + totalDrivingTime);


    }

    public InputFileData FileReaderExample(String inputFile) {

        ClassLoader classLoader = MainTest.class.getClassLoader();
        String filePath = inputFile; // Change this to match the actual path of your file
        InputStream inputStream = classLoader.getResourceAsStream(filePath);

        InputFileData inputFileData = new InputFileData();

        LocalDateTime iniTime = LocalDateTime.of(1970, 1, 1, 0, 0);

        try (BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream))) {
            String line;
            List<Integer> lineInt;
//            transactionList = new ArrayList<>();
            Long currentId = 0L;

            // skip first 4
            for (int i = 0; i < 4; i++) {
                reader.readLine();
            }

            // header
            lineInt = extractIntegers(reader.readLine());
            inputFileData.nrVehicles = lineInt.get(0);
            inputFileData.capacity = lineInt.get(1);

            // skip 4 lines
            for (int i = 0; i < 4; i++) {
                reader.readLine();
            }

            lineInt = extractIntegers(reader.readLine());
            String depotId = "Depot-" + lineInt.get(0).toString();
            int lat = lineInt.get(1);
            int lon = lineInt.get(2);
            LocalDateTime startDateTime = getTime(lineInt.get(4));
            LocalDateTime endDateTime = getTime(lineInt.get(5));
            Location depotLocation = new Location(lat, lon);

            inputFileData.depot = new Depot(depotId, depotLocation);
            inputFileData.startDateTime = startDateTime;
            inputFileData.endDateTime = endDateTime;

            while ((line = reader.readLine()) != null) {

                lineInt = extractIntegers(line);

                if (lineInt.size() > 0) {

                    String customerId = "Customer-" + lineInt.get(0).toString();
                    lat = lineInt.get(1);
                    lon = lineInt.get(2);
                    int demand = lineInt.get(3);
                    LocalDateTime readyTime = getTime(lineInt.get(4));
                    LocalDateTime dueDate = getTime(lineInt.get(5) + lineInt.get(6));
                    Duration serviceDuration = Duration.ofSeconds((long) lineInt.get(6));
                    Location location = new Location(lat, lon);

                    Customer customer = new Customer(customerId, customerId, location, readyTime, dueDate, serviceDuration);

                    inputFileData.customersList.add(customer);

                }
            }

        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        return inputFileData;


    }

    public static LocalDateTime getTime(Integer time) {
        LocalDateTime iniTime = LocalDateTime.of(1970, 1, 1, 0, 0);
        return iniTime.plusSeconds(time);
    }

    public static List<Integer> extractIntegers(String input) {
        List<Integer> integers = new ArrayList<>();

        // Define a regular expression to match integers
        String regex = "\\b\\d+\\b";
        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(input);

        while (matcher.find()) {
            int value = Integer.parseInt(matcher.group());
            integers.add(value);
        }

        return integers;
    }

    class InputFileData {
        public int nrVehicles;
        public int capacity;
        public Depot depot;
        LocalDateTime startDateTime;
        LocalDateTime endDateTime;
        public List<Customer> customersList = new ArrayList<>();

        public InputFileData() {
        }
    }
}




