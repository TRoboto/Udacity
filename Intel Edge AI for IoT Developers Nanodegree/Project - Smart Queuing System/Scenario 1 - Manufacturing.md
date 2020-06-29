# Scenario 1: Manufacturing Sector

Below is the first scenario. Your job is to read through the scenario and figure out which type of hardware might best fit the client's needs. You'll see that this is similar to scenarios you practiced with earlier in the course.

The scenario is pretty long and not all of the information is important! That's intentional and not unlike what you'll encounter when working with real clients. **This is an opportunity to demonstrate that you know which pieces of information are relevant when selecting hardware, and which are unimportant or unrelated.**


## The Scenario

Mr. Vishwas is the VP of Engineering at Naomi Semiconductors, a manufacturer known for its industrial-grade standard in producing semiconductor chips. Recently, the company has been venturing into _Intel Pentium 4/3000_ chip production—and they want to maximize their revenue in this venture. Their other chips in the last year have earned them two million dollars alone. With such good revenue, their expansion into the Intel Pentium 4/3000 industry is an obvious next step.

There are several steps involved in the chip manufacturing process:

*   Step 1: Produce a silicon ingot
*   Step 2: Create blank wafers
*   Step 3: Use these wafers to reproduce a patterned wafer
*   Step 4: Create and test dies
*   Step 5: Assemble bond dies into packages
*   Step 6: Test packaged dies
*   Step 7: Ship dies to customers

Mr. Vishwas explains that there have been several roadblocks in this pipeline. The entire process should take around 6 to 8 weeks—but currently, it is taking 10 to 12 weeks. This is reducing their revenue by 30%.

Mr. Vishwas has noticed that Step 7 (shipping to customers) seems to be taking the most time. This part of the process involves the manual labor of packaging the chips into boxes. There is one particular shop floor—which has two industrial belts—that has shown slower production than the rest.

Workers alternate shifts to keep the floor running 24 hours a day so that packaging continues nonstop, but Mr. Vishwas has noticed a slow-down in production during the shift transition periods. Between shifts, he has observed a 70% dip in the production rate of packaged containers.

To help understand and address these issues, Mr. Vishwas wants a system to monitor the number of people in the factory line. The factory has a vision camera installed at every belt. Each camera records video at 30-35 FPS (Frames Per Second) and this video stream can be used to monitor the number of people in the factory line. Mr. Vishwas would like the image processing task to be completed five times per second.

Once this productivity problem has been addressed, Mr. Vishwas would like to be able to repurpose the system to address a second issue. The second issue Mr. Vishwas has encountered is that a significant percentage of the semiconductor chips being packaged for shipping have flaws. These are not detected until the chips are used by clients. If these flaws could be detected prior to packaging, this would save money and improve the company's reputation.

To be able to detect chip flaws without slowing down the packaging process, the system would need to be able to run inference on the video stream very quickly. Additionally, because there are multiple chip designs—and new designs are created regularly—the system would also need to be flexible so that it can be reprogrammed and optimized to quickly detect flaws in different chip designs.

While Naomi Semiconductors has plenty of revenue to install a quality system, this is still a significant investment and they would ideally like it to last for at least 5-10 years.