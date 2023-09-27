

```java
LocalDate joiningDateLocal = joiningDate.toInstant().atZone(ZoneId.systemDefault())
        .toLocalDate();
    LocalDate today = LocalDate.now(clock);
    return joiningDateLocal.plusDays(daysToCheckJoinDate).isAfter(today);
```